from flask import Flask, render_template_string, request, jsonify
from rag_system import RAGSystem

app = Flask(__name__)


rag_system = RAGSystem()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Pedagogy Suggestion System</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }
        
        button:hover {
            background: #5a6fd8;
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            display: none;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            display: none;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            display: none;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding: 15px;
            background: #e9ecef;
            border-radius: 5px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Pedagogy Suggestion System</h1>
        
        <form id="suggestionForm">
            <div class="input-group">
                <label for="courseName">Course Name:</label>
                <input type="text" id="courseName" placeholder="Enter course name (e.g., Machine Learning, Data Structures)" required>
            </div>
            
            <button type="submit" id="submitBtn">Get Suggestions</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating suggestions...</p>
        </div>
        
        <div class="error" id="error"></div>
        <div class="success" id="success"></div>
        
        <div class="result" id="result">
            <h3 id="courseTitle"></h3>
            <div id="suggestions"></div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number" id="queryTime">0.9s</div>
                    <div class="stat-label">Query Time</div>
                </div>
                <div class="stat">
                    <div class="stat-number" id="apiTime">1.1s</div>
                    <div class="stat-label">API Time</div>
                </div>
                <div class="stat">
                    <div class="stat-number" id="totalTime">2.0s</div>
                    <div class="stat-label">Total Time</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('suggestionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const courseName = document.getElementById('courseName').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            const success = document.getElementById('success');
            
            if (!courseName) {
                showError('Please enter a course name');
                return;
            }
            
            // Show loading, hide others
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            loading.style.display = 'block';
            result.style.display = 'none';
            error.style.display = 'none';
            success.style.display = 'none';
            
            try {
                const response = await fetch('/get_suggestions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ course_name: courseName })
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    showResult(data.course_name, data.suggestions);
                    showSuccess('Suggestions generated successfully!');
                } else {
                    showError(data.error || 'An error occurred');
                }
            } catch (err) {
                showError('Network error. Please try again.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Get Suggestions';
                loading.style.display = 'none';
            }
        });
        
        function showResult(courseName, suggestions) {
            document.getElementById('courseTitle').textContent = `Recommendations for ${courseName}`;
            document.getElementById('suggestions').innerHTML = formatSuggestions(suggestions);
            document.getElementById('result').style.display = 'block';
        }
        
        function formatSuggestions(suggestions) {
            // Simple formatting - just split by double newlines
            const paragraphs = suggestions.split('\\n\\n').filter(p => p.trim());
            return paragraphs.map(p => `<p>${p}</p>`).join('');
        }
        
        function showError(message) {
            const error = document.getElementById('error');
            error.textContent = message;
            error.style.display = 'block';
        }
        
        function showSuccess(message) {
            const success = document.getElementById('success');
            success.textContent = message;
            success.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        data = request.get_json()
        course_name = data.get('course_name', '').strip()
        
        if not course_name:
            return jsonify({'error': 'Please enter a course name'}), 400
        
       
        suggestions = rag_system.generate_suggestion(course_name)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'course_name': course_name
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 