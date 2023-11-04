import React from 'react';
import {Box} from '@mui/material';
import Message, {MessageProps} from "./Message";


interface ChatProps {
    messages:  MessageProps[];
    user: any;
}

const Chat: React.FC<ChatProps> = ({messages, user}) => {
    return (
        <Box mt={3} sx={{gap:'1rem'}}>
            {messages.map((message, index) => (
                <Message key={index} role={message.role} content={message.content} sources={message.sources} user={user}/>
            ))}
        </Box>
    );
};

export default Chat;
