import "./App.css";

import axios from "axios";
import React, { useEffect, useState } from "react";

import EmojiPeopleIcon from "@mui/icons-material/EmojiPeople";
import SearchIcon from "@mui/icons-material/Search";
import { Box, Button, InputAdornment, TextField, Typography } from "@mui/material";

import Chat from "./Chat";
import Message, { MessageProps } from "./Message";

let domain = window.location.origin;

function App() {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState<MessageProps[]>([]);
    const [transcript, setTranscript] = useState<MessageProps[]>([]);

    const handleQuery = async () => {
        setLoading(true);
        setInput("Torstone Intelligence is working on your query...");
        messages.push({ role: "DOCTOR", content: input });
        const result = await axios.post(`${domain}/query`, { chat_history: messages, transcript: transcript });
        let chatHistory = result.data.response.chat_history;
        setMessages(chatHistory);
        setLoading(false);
        setInput("");
    };

    const uploadTranscript = async () => {
        console.log("uploading transcript");
        let transcript = [
            { role: "DOCTOR", content: "Hello, I am Dr. Smith. How can I help you today?" } as MessageProps,
            { role: "PATIENT", content: "I have a headache." } as MessageProps,
            { role: "DOCTOR", content: "How long have you had this headache?" } as MessageProps,
            { role: "PATIENT", content: "About 3 days." } as MessageProps,
            {
                role: "DOCTOR",
                content:
                    "How long have you had this headache? How long have you had this headache? How long have you had this headache? How long have you had this headache? How long have you had this headache? ",
            } as MessageProps,
            { role: "PATIENT", content: "I have a headache." } as MessageProps,
            { role: "DOCTOR", content: "How long have you had this headache?" } as MessageProps,
            { role: "PATIENT", content: "About 3 days." } as MessageProps,
            {
                role: "DOCTOR",
                content:
                    "How long have you had this headache? How long have you had this headache? How long have you had this headache? How long have you had this headache? How long have you had this headache? ",
                sources: [{ source: "https://www.google.com", title: "Google" }],
            } as MessageProps,
        ];
        setTranscript(transcript);
    };

    const classN = loading ? "gradient-border" : "";
    return (
        <Box pb={"5%"}>
            <Box display={"flex"} justifyContent={"space-between"} mt={1} p={2}>
                <Box display={"flex"} alignItems={"center"}>
                    <EmojiPeopleIcon sx={{ fontSize: "2.5rem" }} />
                </Box>
                <Box display={"flex"} className={"logout-button"}>
                    <Button sx={{ fontSize: "16px" }} onClick={uploadTranscript} color={"secondary"}>
                        Upload transcript
                    </Button>
                </Box>
            </Box>
            <Box pl={"15%"} pr={"15%"} mt={"5%"}>
                <Typography variant={"h2"} fontSize={"calc(1.6rem + 2   vw)"} fontWeight={800} mb={4}>
                    Junior Doctor
                </Typography>
                <Box display="flex" position={"relative"}>
                    <Box sx={{ backgroundColor: "primary.main", borderRadius: "0.5em" }} width={"50%"} p={2} mr={1} overflow={"auto"}>
                        <Typography variant={"h4"} display={"block"} fontSize={"calc(1.6rem + 2   vw)"} fontWeight={800}>
                            Transcript
                        </Typography>
                        <Box sx={{ borderRadius: "0.5em" }} overflow={"auto"} maxHeight={500}>
                            <Chat messages={transcript} />
                        </Box>
                    </Box>
                    <Box sx={{ backgroundColor: "primary.main", borderRadius: "0.5em" }} width={"50%"} p={2} ml={1}>
                        <Typography variant={"h4"} display={"block"} fontSize={"calc(1.6rem + 2   vw)"} fontWeight={800}>
                            Conversation
                        </Typography>
                        <Box sx={{ borderRadius: "0.5em" }} overflow={"auto"} maxHeight={500}>
                            <Chat messages={messages} />
                        </Box>
                    </Box>
                </Box>
                <Box maxWidth={"100%"} mt={5}>
                    <TextField
                        id="outlined-basic"
                        variant="outlined"
                        value={input}
                        className={classN}
                        placeholder="Ask a question..."
                        style={{ fontStyle: "italic" }} // Italicized placeholder
                        onChange={(e) => setInput(e.target.value)}
                        InputProps={{
                            style: { height: "4rem" },
                            startAdornment: (
                                <InputAdornment position="start">
                                    <SearchIcon />
                                </InputAdornment>
                            ),
                        }}
                        fullWidth
                        sx={{ "& fieldset": loading ? { border: "none" } : { border: "3px solid gray" } }}
                    />
                    <Button variant="contained" sx={{ mt: 2 }} color={"secondary"} onClick={handleQuery}>
                        Get Answer
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

export default App;
