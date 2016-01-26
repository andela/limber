html_email = """
<!DOCTYPE html>
<html>
<head>
	<title>Project Invitation</title>
	<style type="text/css">

		body {
			font-family: Arial;
			font-size: 1.5em;
			text-align: left;
		}

		span {
			background-color: #e0e0e0;
		}

		a {
			border: 1px solid #2196F3;
			padding: 1.2em 1.5em;
			margin: 1em auto;
			background: #2196F3;
			border-radius: 3px;
			color: #fff;
			display: inline-block;
			text-decoration: none;
		}

		a:hover {
			cursor: pointer;
		}

		#main {
			margin: auto;
			padding: 2em;
			width: 55em;
			border-style: solid;
			border-color: #80d8ff;
		}

		#url{
			text-align: center;
		}

		img {
			width: 3em;
			height: 3em;
		}

		#letter_head img {
			display: block;
			margin: 0 auto;
			padding-bottom: 1em;
		}
	</style>
</head>
<body>
	<div id="main">
		<div id="letter_head">
			<img src="https://github.com/andela/limber/blob/develop/static/images/logo.png?raw=true">
		</div>
		<p id="salutation">Hi there,</p>
		<p> <strong>%s</strong> has invited you to collaborate on project <span>%s</span> on Limber.</p>
		<p>Limber is a project management platform for Agile perfectionists with deadlines.</p>
		<p>To accept this invitation, click on the button below.</p>

		<div id="url">
			<a href=%s >Accept Invite</a>
		</div>

		<p>If you have received this email in error, please ignore it.</p>
		<p>Thanks!</p>
		<p>- The Limber Team.</p>
	</div>
</body>
</html>
"""