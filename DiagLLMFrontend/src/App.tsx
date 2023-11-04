import "./App.css";

import axios from "axios";
import { jwtDecode } from "jwt-decode";
import React, { useEffect, useState } from "react";

import EmojiPeopleIcon from "@mui/icons-material/EmojiPeople";
import SearchIcon from "@mui/icons-material/Search";
import { Box, Button, InputAdornment, TextField, Typography } from "@mui/material";

import Chat from "./Chat";
import { write_to_log } from "./global"; // import dependency
import LoginForm from "./LoginForm";
import { MessageProps } from "./Message";

function sleep(time: number) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function App() {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState<MessageProps[]>([]);
    const [loggedIn, setLoggedIn] = useState(false);
    const user = JSON.parse(localStorage.getItem("user") as any | {});

    async function googleLogin(token: string) {
        const decoded = jwtDecode(token) as any;
        localStorage.setItem("user", JSON.stringify(decoded));
        write_to_log(`${decoded.name} has logged in to Torstone Intelligence`);
        setLoggedIn(true);
    }

    function clearCookie(cookieName: string) {
        // Set the cookie to expire in the past (i.e., instantly clear it)
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    }

    function extractGStateCookie(cookieString: string) {
        // Define a regex pattern to match the "g_state" cookie
        const regex = /g_state=([^;]+)/;

        // Use the regex pattern to search for the "g_state" cookie
        const match = cookieString.match(regex);

        // Check if a match is found
        if (match) {
            // The cookie value is captured in the first group of the match
            return match[1];
        } else {
            // If no match is found, return null or handle accordingly
            return null;
        }
    }

    function isUserLoggedIn() {
        return extractGStateCookie(document.cookie) !== null;
    }

    const getChatHistory = async () => {
        const result = await axios.get("http://localhost:5000/chat-history");
        setMessages(result.data.response);
    };

    const handleQuery = async () => {
        setLoading(true);
        setInput("Torstone Intelligence is working on your query...");
        write_to_log(`${user.name} has asked the following question to Torstone Intelligence: ${input}`);
        const result = await axios.post("http://localhost:5000/query", { query: input });
        let chatHistory = result.data.response.chat_history;
        chatHistory[chatHistory.length - 1].sources = result.data.response.sources;
        setMessages(chatHistory);
        setLoading(false);
        setInput("");
    };

    useEffect(() => {
        getChatHistory();
        setLoggedIn(isUserLoggedIn());
    });

    const classN = loading ? "gradient-border" : "";
    return !loggedIn ? (
        <LoginForm onGoogleLogin={googleLogin} />
    ) : (
        <Box pb={"5%"}>
            <Box display={"flex"} justifyContent={"space-between"} mt={1} p={2}>
                <Box display={"flex"} alignItems={"center"}>
                    <EmojiPeopleIcon sx={{ fontSize: "2.5rem" }} />
                    <Typography variant={"h6"} ml={1}>
                        {user["name"]}
                    </Typography>
                </Box>
                <Box display={"flex"} className={"logout-button"}>
                    <Button
                        sx={{ fontSize: "16px" }}
                        onClick={() => {
                            clearCookie("g_state");
                            setLoggedIn(false);
                        }}
                    >
                        Log out
                    </Button>
                </Box>
            </Box>
            <Box pl={"15%"} mt={"5%"}>
                <Typography variant={"h2"} fontSize={"calc(1.6rem + 2   vw)"} fontWeight={800}>
                    Torstone Intelligence
                </Typography>
                <Box maxWidth={"75%"}>
                    <Chat messages={messages} user={user} />
                </Box>
                <Box maxWidth={"75%"} mt={5}>
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
                    <Button variant="contained" sx={{ mt: 2 }} onClick={handleQuery}>
                        Get Answer
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

export default App;
