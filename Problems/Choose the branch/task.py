template = """
<html>
  <div>{% if post.author %} {{post.text}} {% else %}
    {% endif %}
  </div>
</html>
"""