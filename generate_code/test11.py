from flask import Flask, render_template_string, request

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <title>Email Composer</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    textarea { width: 100%; height: 150px; }
    .email-preview { margin-top: 30px; padding: 15px; border: 1px solid #ccc; background: #f9f9f9; }
  </style>
</head>
<body>
  <h1>Compose Your Email</h1>
  <form method="post">
    <label for="subject">Subject:</label><br>
    <input type="text" name="subject" id="subject" style="width:100%;" value="{{ subject }}"><br><br>
    
    <label for="body">Body:</label><br>
    <textarea name="body" id="body">{{ body }}</textarea><br><br>
    
    <button type="submit">Preview Email</button>
  </form>

  {% if subject or body %}
  <div class="email-preview">
    <h2>{{ subject }}</h2>
    <p>{{ body.replace('\\n', '<br>')|safe }}</p>
  </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def compose():
    subject = ""
    body = ""
    if request.method == "POST":
        subject = request.form.get("subject", "")
        body = request.form.get("body", "")
    return render_template_string(TEMPLATE, subject=subject, body=body)

if __name__ == "__main__":
    app.run(debug=True)
