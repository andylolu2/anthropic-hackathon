import React from "react";

import { Box } from "@mui/material";

import Message, { MessageProps } from "./Message";

interface ChatProps {
    messages: MessageProps[];
}

const Chat: React.FC<ChatProps> = ({ messages }) => {
    return (
        <Box sx={{ gap: "1rem" }}>
            {messages.map((message, index) => (
                <Message key={index} role={message.role} content={message.content} sources={message.sources} />
            ))}
        </Box>
    );
};

export default Chat;
