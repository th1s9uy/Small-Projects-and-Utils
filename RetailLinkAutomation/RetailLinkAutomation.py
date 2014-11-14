import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; MS-RTC EA 2')]

reponse = br.open("https://rllogin.wal-mart.com/rl_security/rl_logon.aspx?ServerType=IIS1&CTAuthMode=BASIC&CTLoginErrorMsg=BAD_PWD_OR_USER&language=en&CTUser=&CT_ORIG_URL=%2Frl_security%2Frl_logon.aspx%3FServerType%3DIIS1%26redir%3D%2F&ct_orig_uri=%2Frl_security%2Frl_logon.aspx")