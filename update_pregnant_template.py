import os

filepath = r"c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated\core\templates\core\pregnant_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_section = '''    <!-- Pregnancy Tips Card (below planning section) -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-success h-100 reveal">
                <div class="card-header bg-success text-white py-3">
                    <h5 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Pregnancy Tips</h5>
                </div>
                <div class="card-body text-center">
                    <p class="text-muted mb-3">Get personalized Do's and Don'ts for your pregnancy journey</p>
                    <a href="{% url 'trimester_tips' %}" class="btn btn-success">
                        <i class="fas fa-list me-2"></i>View All Trimester Tips
                    </a>
                </div>
            </div>
        </div>
    </div>'''

new_section = '''    <!-- Trimester-Specific Personalized Recommendations -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-warning h-100 reveal">
                <div class="card-header bg-warning text-dark py-3">
                    <h5 class="mb-0">
                        <i class="fas fa-star me-2"></i>
                        {% if trimester_info.name %}
                            {{ trimester_info.name }} Recommendations ({{ trimester_info.weeks }})
                        {% else %}
                            Personalized Recommendations for Trimester {{ current_trimester }}
                        {% endif %}
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <!-- Trimester Tips -->
                        <div class="col-md-4 mb-3">
                            <div class="card border-success h-100">
                                <div class="card-header bg-success text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Tips for You</h6>
                                </div>
                                <div class="card-body">
                                    {% if trimester_info.tips %}
                                        <ul class="list-unstyled mb-0">
                                            {% for tip in trimester_info.tips %}
                                                <li class="mb-2">
                                                    <i class="fas fa-check-circle text-success me-2"></i>{{ tip }}
                                                </li>
                                            {% endfor %}
                                        </ul>
                                    {% else %}
                                        <p class="text-muted">Loading trimester tips...</p>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Diet Recommendations -->
                        <div class="col-md-4 mb-3">
                            <div class="card border-info h-100">
                                <div class="card-header bg-info text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-utensils me-2"></i>Diet Plan</h6>
                                </div>
                                <div class="card-body">
                                    {% if diet_content %}
                                        {% for content in diet_content|slice:":3" %}
                                            <div class="mb-2 pb-2 {% if not forloop.last %}border-bottom{% endif %}">
                                                <strong class="small">{{ content.title }}</strong>
                                                <p class="text-muted small mb-0">{{ content.body|truncatewords:12 }}</p>
                                            </div>
                                        {% endfor %}
                                        <a href="{% url 'diet_plans' %}" class="btn btn-sm btn-outline-info w-100 mt-2">View All</a>
                                    {% else %}
                                        <p class="text-muted small">No diet plans for this trimester yet.</p>
                                        <a href="{% url 'diet_plans' %}" class="btn btn-sm btn-outline-info">Browse All</a>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Exercise Recommendations -->
                        <div class="col-md-4 mb-3">
                            <div class="card border-danger h-100">
                                <div class="card-header bg-danger text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-running me-2"></i>Exercise</h6>
                                </div>
                                <div class="card-body">
                                    {% if exercise_content %}
                                        {% for content in exercise_content|slice:":3" %}
                                            <div class="mb-2 pb-2 {% if not forloop.last %}border-bottom{% endif %}">
                                                <strong class="small">{{ content.title }}</strong>
                                                <p class="text-muted small mb-0">{{ content.body|truncatewords:12 }}</p>
                                            </div>
                                        {% endfor %}
                                        <a href="{% url 'exercise_guidance' %}" class="btn btn-sm btn-outline-danger w-100 mt-2">View All</a>
                                    {% else %}
                                        <p class="text-muted small">No exercises for this trimester yet.</p>
                                        <a href="{% url 'exercise_guidance' %}" class="btn btn-sm btn-outline-danger">Browse All</a>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="text-center mt-3">
                        <a href="{% url 'trimester_tips' %}" class="btn btn-warning">
                            <i class="fas fa-list me-2"></i>View Complete Trimester Guide
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>'''

# Try with different line endings
content_lf = content.replace('\r\n', '\n')
old_section_lf = old_section.replace('\r\n', '\n')

if old_section in content:
    content = content.replace(old_section, new_section)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Updated pregnant_dashboard.html with trimester recommendations!")
elif old_section_lf in content_lf:
    content_lf = content_lf.replace(old_section_lf, new_section.replace('\r\n', '\n'))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_lf)
    print("SUCCESS: Updated pregnant_dashboard.html (with normalized line endings)")
else:
    print("Could not find the old section. Checking for partial match...")
    if "Pregnancy Tips Card" in content:
        print("Found 'Pregnancy Tips Card' - the comment exists but format differs")
    else:
        print("Did not find the section at all")
