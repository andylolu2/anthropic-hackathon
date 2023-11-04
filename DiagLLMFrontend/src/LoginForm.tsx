import React, {FormEvent} from 'react';
import {Box, Typography} from "@mui/material";
import {GoogleLogin, GoogleOAuthProvider} from "@react-oauth/google";

interface LoginFormProps {
    onGoogleLogin: (token: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({onGoogleLogin}) => {

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
    };

    return (
        <form onSubmit={handleSubmit}>
            <Box pl={'15%'} mt={'5%'}>
                <Typography variant={'h3'}>Login to Torstone Intelligence</Typography>
                <Box mt={1}>
                    <GoogleOAuthProvider
                        clientId={"967512379868-rik098kdsujjc81db6ohqpbn42d2kc6v.apps.googleusercontent.com"}>
                        <GoogleLogin
                            onSuccess={(credentialResponse: any) => {
                                onGoogleLogin(credentialResponse.credential);
                            }}
                            onError={() => {
                                console.log('Login Failed');
                            }}
                        />
                    </GoogleOAuthProvider>
                </Box>
            </Box>

        </form>
    );
};

export default LoginForm;
