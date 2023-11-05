import "./App.css";

import axios from "axios";
import React, { useState } from "react";

import EmojiPeopleIcon from "@mui/icons-material/EmojiPeople";
import SearchIcon from "@mui/icons-material/Search";
import { Box, Button, InputAdornment, LinearProgress, TextField, Typography } from "@mui/material";

import Chat from "./Chat";
import data from "./data_bad.json";
import { MessageProps } from "./Message";

let domain = window.location.origin;

function App() {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState<MessageProps[]>([]);
    const [transcript, setTranscript] = useState<MessageProps[]>([]);

    const handleQuery = async () => {
        setLoading(true);
        setInput("Junior doctor is working on your query...");
        messages.push({ role: "DOCTOR", content: input });
        try {
            const result = await axios.post(`${domain}/query`, { chat_history: messages, transcript: transcript });
            let chatHistory = result.data.response.chat_history;
            setMessages(chatHistory);
        } catch (error) {
            console.log(error);
        } finally {
            setInput("");
            setLoading(false);
        }
    };

    const uploadTranscript = async () => {
        setTranscript(data);
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
                    HealthEcho
                </Typography>
                <Box display="flex" position={"relative"}>
                    <Box sx={{ backgroundColor: "primary.main", borderRadius: "0.5em" }} width={"50%"} p={3} mr={2} overflow={"auto"}>
                        <Typography variant={"h4"} display={"block"} fontSize={"calc(1.6rem + 2   vw)"} fontWeight={800} mb={2}>
                            Transcript
                        </Typography>
                        <Box sx={{ borderRadius: "0.5em" }} overflow={"auto"} maxHeight={500}>
                            <Chat messages={transcript} />
                        </Box>
                    </Box>
                    <Box sx={{ backgroundColor: "primary.main", borderRadius: "0.5em" }} width={"50%"} p={3} ml={2}>
                        <Typography variant={"h4"} display={"block"} fontSize={"calc(1.6rem + 2   vw)"} fontWeight={800} mb={2}>
                            Conversation
                        </Typography>
                        <Box sx={{ borderRadius: "0.5em" }} overflow={"auto"} maxHeight={500}>
                            <Chat messages={messages} />
                        </Box>
                    </Box>
                </Box>
                <Box maxWidth={"100%"} mt={5}>
                    {loading ? (
                        <LinearProgress />
                    ) : (
                        <TextField
                            id="outlined-basic"
                            variant="outlined"
                            value={input}
                            className={classN}
                            placeholder="Ask a question..."
                            style={{ fontStyle: "italic" }} // Italicized placeholder
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                    handleQuery();
                                }
                            }}
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
                    )}
                </Box>
            </Box>
        </Box>
    );
}

export default App;
