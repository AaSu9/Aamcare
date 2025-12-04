import os

filepath = r"c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated\core\templates\core\mother_dashboard.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the position after the postpartum planning section (line 93)
# and before the row div (line 95)
old_text = '''    </div>

    <div class="row">
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fas fa-chart-line me-2"></i>Recovery Progress</h5>'''

new_text = '''    </div>

    <!-- Postpartum Stage-Specific Personalized Recommendations -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-warning h-100">
                <div class="card-header bg-warning text-dark py-3">
                    <h5 class="mb-0">
                        <i class="fas fa-star me-2"></i>
                        {% if stage_info.name %}
                            {{ stage_info.name }} Recommendations ({{ stage_info.period }})
                        {% else %}
                            Personalized Recommendations for Your Recovery Stage
                        {% endif %}
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <!-- Stage Tips -->
                        <div class="col-md-3 mb-3">
                            <div class="card border-success h-100">
                                <div class="card-header bg-success text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Tips</h6>
                                </div>
                                <div class="card-body">
                                    {% if stage_info.tips %}
                                        <ul class="list-unstyled mb-0 small">
                                            {% for tip in stage_info.tips %}
                                                <li class="mb-2">
                                                    <i class="fas fa-check-circle text-success me-1"></i>{{ tip }}
                                                </li>
                                            {% endfor %}
                                        </ul>
                                    {% else %}
                                        <p class="text-muted small">Loading tips...</p>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Diet Recommendations -->
                        <div class="col-md-3 mb-3">
                            <div class="card border-info h-100">
                                <div class="card-header bg-info text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-utensils me-2"></i>Diet</h6>
                                </div>
                                <div class="card-body">
                                    {% if diet_content %}
                                        {% for content in diet_content|slice:":2" %}
                                            <div class="mb-2 pb-2 {% if not forloop.last %}border-bottom{% endif %}">
                                                <strong class="small">{{ content.title }}</strong>
                                                <p class="text-muted small mb-0">{{ content.body|truncatewords:10 }}</p>
                                            </div>
                                        {% endfor %}
                                        <a href="{% url 'comprehensive_nutrition_mother' %}" class="btn btn-sm btn-outline-info w-100 mt-1">View All</a>
                                    {% else %}
                                        <p class="text-muted small">No diet plans for this stage yet.</p>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Exercise Recommendations -->
                        <div class="col-md-3 mb-3">
                            <div class="card border-danger h-100">
                                <div class="card-header bg-danger text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-running me-2"></i>Exercise</h6>
                                </div>
                                <div class="card-body">
                                    {% if exercise_content %}
                                        {% for content in exercise_content|slice:":2" %}
                                            <div class="mb-2 pb-2 {% if not forloop.last %}border-bottom{% endif %}">
                                                <strong class="small">{{ content.title }}</strong>
                                                <p class="text-muted small mb-0">{{ content.body|truncatewords:10 }}</p>
                                            </div>
                                        {% endfor %}
                                        <a href="{% url 'exercise_guidance' %}" class="btn btn-sm btn-outline-danger w-100 mt-1">View All</a>
                                    {% else %}
                                        <p class="text-muted small">No exercises for this stage yet.</p>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Breastfeeding Support -->
                        <div class="col-md-3 mb-3">
                            <div class="card border-primary h-100">
                                <div class="card-header bg-primary text-white py-2">
                                    <h6 class="mb-0"><i class="fas fa-heart me-2"></i>Breastfeeding</h6>
                                </div>
                                <div class="card-body">
                                    {% if breastfeeding_content %}
                                        {% for content in breastfeeding_content|slice:":2" %}
                                            <div class="mb-2 pb-2 {% if not forloop.last %}border-bottom{% endif %}">
                                                <strong class="small">{{ content.title }}</strong>
                                                <p class="text-muted small mb-0">{{ content.body|truncatewords:10 }}</p>
                                            </div>
                                        {% endfor %}
                                        <a href="{% url 'breastfeeding_support' %}" class="btn btn-sm btn-outline-primary w-100 mt-1">View All</a>
                                    {% else %}
                                        <p class="text-muted small">No content for this stage yet.</p>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5><i class="fas fa-chart-line me-2"></i>Recovery Progress</h5>'''

# Normalize line endings for matching
content_lf = content.replace('\r\n', '\n')
old_text_lf = old_text.replace('\r\n', '\n')

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Updated mother_dashboard.html with postpartum recommendations!")
elif old_text_lf in content_lf:
    content_lf = content_lf.replace(old_text_lf, new_text.replace('\r\n', '\n'))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_lf)
    print("SUCCESS: Updated mother_dashboard.html (with normalized line endings)")
else:
    print("Could not find the old section")
    if "Recovery Progress" in content:
        print("Found 'Recovery Progress' in file")
