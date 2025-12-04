import re

filepath = r"c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated\core\templates\core\pregnant_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the unclosed if block after line 30 and add endif before the next anchor tag
old = '''{% if pregnancy_dates.days_remaining <= 0 %}
                                <a href="{% url 'give_birth' %}" class="btn btn-success btn-lg">
                                    <i class="fas fa-baby me-2"></i>{% trans "I've Given Birth" %}
                                </a>
                            <a href="{% url 'update_pregnant_profile' %}'''

new = '''{% if pregnancy_dates.days_remaining <= 0 %}
                                <a href="{% url 'give_birth' %}" class="btn btn-success btn-lg">
                                    <i class="fas fa-baby me-2"></i>{% trans "I've Given Birth" %}
                                </a>
                            {% endif %}
                            <a href="{% url 'update_pregnant_profile' %}'''

if old in content:
    content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed: Added missing {% endif %}")
else:
    print("Pattern not found, trying alternative...")
    # Try with different line endings
    content = content.replace('\r\n', '\n')
    old = old.replace('\r\n', '\n')
    new = new.replace('\r\n', '\n')
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed with normalized line endings!")
    else:
        print("Could not find pattern")
