class RequestConstant:
    MallUserLoginPath = "api/v1/user/login"
    MallUserInfoPath = "api/v1/user/info"
    MallUserRegisterPath = "api/v1/user/register"

    ResultCodeKey = "resultCode"
    DataKey= "data"
    LoginNameKey = "loginName"
    PasswordMD5Key = "passwordMd5"
    PasswordKey = "password"

    @staticmethod
    def login_data(name,password_md5):
        return {
            RequestConstant.LoginNameKey:name,
            RequestConstant.PasswordMD5Key:password_md5
        }
