password_request_email = """
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <table cellpadding="0" cellspacing="0" style="border-radius:4px;border:1px #dceaf5 solid" border="0" align="center">
        <tbody>
            <tr>
                <td colspan="3" height="6"></td>
            </tr>
            <tr style="line-height:0px">
                <td width="100%" style="font-size:0px" align="center" height="1">
                    <img width="40px" style="max-height:73px;width:40px" alt="" src="https://github.com/andela/limber/blob/develop/public/static/images/logo.png?raw=true" class="CToWUd">
                </td>
            </tr>
            <tr>
                <td>
                    <table cellpadding="0" cellspacing="0" style="line-height:25px" border="0" align="center">
                        <tbody>
                            <tr>
                                <td colspan="3" height="30"></td>
                            </tr>
                            <tr>
                                <td width="36"></td>
                                <td width="454" align="left" style="color:#444444;border-collapse:collapse;font-size:11pt;font-family:proxima_nova,'Open Sans','Lucida Grande','Segoe UI',Arial,Verdana,'Lucida Sans Unicode',Tahoma,'Sans Serif';max-width:454px" valign="top">
                                    Hi there,
                                    <br><br><p>Someone recently requested a password change for your Limber account. If this was you, you can set a new password using the button below.</p>
                                    <br>
                                    <br>
                                    <center>
                                        <a style="border-radius:3px;font-size:15px;color:white;border:1px #1373b5 solid;text-decoration:none;padding:14px 7px 14px 7px;width:280px;max-width:280px;font-family:proxima_nova,'Open Sans','lucida grande','Segoe UI',arial,verdana,'lucida sans unicode',tahoma,sans-serif;margin:6px auto;display:block;background-color:#007ee6;text-align:center" href={0} target="_blank">Reset Password</a></center>
                                    <br>
                                    <br>
                                    <p>If you don't want to change your password or didn't request this, just ignore and delete this message.</p>
                                    <p>To keep your account secure, please don't forward this email to anyone.</p>
                                    <br>
                                    <span>Thanks!</span>
                                    <br>
                                    <span>- The <span class="il">Limber</span> Team</span>
                                </td>
                                <td width="36"></td>
                            </tr>
                            <tr>
                                <td colspan="3" height="36"></td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""