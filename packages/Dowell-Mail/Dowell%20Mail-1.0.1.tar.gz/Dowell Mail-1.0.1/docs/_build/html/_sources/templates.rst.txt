home template
=============

The `templates/maillib/home.html` template contains an email form where the user can enter the details for the email they want to send.
Here is how it look:

.. code-block:: html
    :linenos:

    {% extends '_partials/base.html' %}


    {% block title %}
      Home
    {% endblock %}

    {% load static %}


    {% block content %}
    <h1>Home</h1>
    <div class="formcarry-container">
      {% include '_partials/messages.html' %}
      <form method="post" action={% url 'home' %} class="formcarry-form">
          {% csrf_token %}
        <!-- <label for="email">Your API Key</label>
        <input type="text" id="email" name="apiKey" required /> -->
        
        <label for="fullName">Your Name</label>
        <input type="text" id="fullName" name="fullName" required />

        <label for="fromEmail">Your Email Address</label>
        <input type="email" id="fromEmail" name="fromEmail" required />
        
        <label for="toName">Recepient's Name</label>
        <input type="toName" id="toName" name="toName" required />

        <label for="email">Target Email Address</label>
        <input type="email" id="toEmail" name="toEmail" required />

        <label for="subject">Subject</label>
        <input type="text" id="subject" name="subject" required />

        <label for="message">Your Message</label>
        <textarea name="message" id="message" cols="30" rows="10"></textarea>

        <button type="submit">Send</button>
      </form>
    </div>

    {% endblock %}


