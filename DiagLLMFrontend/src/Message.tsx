import React from "react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";

import MedicalInformationIcon from "@mui/icons-material/MedicalInformation";
import MemoryIcon from "@mui/icons-material/Memory";
import PersonIcon from "@mui/icons-material/Person";
import { Box, Link, Typography } from "@mui/material";

export interface MessageProps {
    role: string;
    content: string;
    sources?: any[];
}

export const Message: React.FC<MessageProps> = ({ role, content, sources }) => {
    return (
        <Box
            pl={1}
            borderRadius={"0.5rem"}
            display="flex"
            flexDirection="column"
            alignItems="flex-start"
            mb={2}
            border={"1px solid #DFE1E6"}
            sx={{ backgroundColor: "primary.light" }}
        >
            <Box display={"flex"} px={1} py={2} flexDirection={"row"}>
                {role === "PATIENT" ? (
                    <PersonIcon style={{ fontSize: "2rem", marginRight: "0.5rem" }} />
                ) : role === "DOCTOR" ? (
                    <MedicalInformationIcon style={{ fontSize: "2rem", marginRight: "0.5rem" }} />
                ) : (
                    <MemoryIcon style={{ fontSize: "2rem", color: "#c4272c", marginRight: "0.5rem" }} />
                )}
                <Box
                    sx={{
                        "& > p": {
                            mt: "6px",
                            mb: "0",
                            wordWrap: "break-word",
                            whiteSpace: "pre-wrap",
                        },
                    }}
                >
                    <ReactMarkdown remarkPlugins={[gfm]} children={content} />
                </Box>
            </Box>
            {sources && (
                <Box mt={1} pl={2}>
                    <Typography variant={"body1"} fontWeight={"bold"} mb={0}>
                        {" "}
                        Sources:{" "}
                    </Typography>
                    <ul style={{ whiteSpace: "nowrap", margin: 0 }}>
                        {sources.map((source, index) => (
                            <li>
                                <Box key={index} mb={1} py={1} pl={2}>
                                    <Link key={index} href={source.source} color="secondary.main">
                                        {source.title}{" "}
                                    </Link>
                                </Box>
                            </li>
                        ))}
                    </ul>
                </Box>
            )}
        </Box>
    );
};

export default Message;
