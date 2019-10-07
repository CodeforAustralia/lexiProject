# Welcome to Lexi Project!

**Lexi** is a system (Django web app) that helps us to our *Lexicon*. Lexi validates any message or communication before sending it to other people such as customers.

## What Lexi does?
Easy! It gets a text, analyzes it, and validates each word to determine whether that word is a common or uncommon word. Then, based on how common each word is, Lexi presents the same text but, additionally, highlights each word with a color tag explaining how common each word is. Lexi also indicates how accessible text is by showing with each message a percentile reading. A message will be green if your use of common words rate higher or equal to 80%. Otherwise, the message will be in red, asking the user to double-check the message. As charts are the best way to show results in a summarized form, Lexi also draws a pie chart with the percentages for both the common and uncommon words.

## How it works?
As mentioned above, Lexi is a Django web app. So there are some preconditions we need to have before using Lexi.

### Install Python and Django

- [Python 3]([https://www.python.org/](https://www.python.org/)) needs to be installed in the laptop / server you are using to run Lexi. Make sure you have **Python 3.7.4+**.
	> If you already have Python 3 installed, check its version.
    `$	python --version`

- [Django](https://www.djangoproject.com/) is the next thing you need to have installed. Verify you have **Django 2.2.5+**.
	> You can validate this with the next command.
	`$ pip show django`

### Clone *Lexi Project* from Git Hub