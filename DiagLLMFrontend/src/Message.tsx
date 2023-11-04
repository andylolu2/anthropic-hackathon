import React, {useState} from "react";
import {Box, IconButton, Link, Typography} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import MemoryIcon from '@mui/icons-material/Memory';
import ReactMarkdown from 'react-markdown';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
import ThumbDownOffAltIcon from '@mui/icons-material/ThumbDownOffAlt';
import gfm from 'remark-gfm';
import {write_to_log} from "./global";

export interface MessageProps {
    role: 'HUMAN' | 'AI';
    content: string;
    sources?: any[];
    user: any,
}

export const Message: React.FC<MessageProps> = ({role, content, sources, user}) => {
    const isUser = role === 'HUMAN';
    const [activeButton, setActiveButton] = useState("");

    return (
        <Box
            py={'1rem'}
            pl={2}
            borderRadius={'0.5rem'}
            display="flex"
            flexDirection="column"
            alignItems="flex-start"
            mb={3}
            border={'2px solid #DFE1E6'}
            boxShadow={'0 0.4rem 0.8rem rgba(9,30,66,0.5)'} // Enhanced shadow
        >
            <Box display={'flex'} p={2}
                 mb={'-1rem'} flexDirection={'row'} sx={{
                "& > *": {
                    'my': '0.5rem',
                }
            }}>
                {isUser ? <PersonIcon style={{fontSize: '2rem', marginRight: '0.5rem'}}/> :
                    <MemoryIcon
                        style={{fontSize: '2rem', color: '#c4272c', marginRight: '0.5rem'}}/>}
                <Box sx={{
                    "& > p": {
                        'mt': '0',
                    }
                }}>
                    <ReactMarkdown
                        remarkPlugins={[gfm]}
                        children={content}
                    />
                </Box>
            </Box>
            {
                sources &&
                <Box mt={4} pl={2}>
                    <Typography variant={'body1'} fontWeight={'bold'}> Sources: </Typography>
                    <ul style={{whiteSpace: 'nowrap', margin: 0}}>
                        {
                            sources.map((source, index) => (
                                <li>
                                    <Box key={index}
                                         mb={1}
                                         py={1}
                                         pl={2}
                                        // Alternating background colors:
                                         bgcolor={index % 2 === 0 ? 'rgba(220, 220, 220, 0.5)' : 'transparent'}
                                         style={{marginTop: '10px'}}>
                                        <Link key={index} href={source.source}> {source.title} </Link>
                                    </Box>
                                </li>
                            ))
                        }
                    </ul>
                </Box>
            }

            {role === 'AI' &&
                <Box p={2}
                     display="flex"
                     alignItems="center"
                     justifyContent="center"
                     width={'100%'}>
                    <Typography variant="body1">Was this helpful?</Typography>
                    <Box display="flex" alignItems="center">
                        <IconButton
                            size="small"
                            sx={{ml: 1}} 
                            color={activeButton === 'like' ? 'success' : 'default'}
                            onClick={() => {
                                setActiveButton('like')
                                write_to_log(`${user.name} liked the following message: ${content}`)
                            }}
                        >
                            <ThumbUpOffAltIcon fontSize="small"/>
                        </IconButton>
                        <Typography variant="body2">Yes</Typography>
                        <IconButton
                            size="small"
                            sx={{ml: 1}}
                            color={activeButton === 'dislike' ? 'error' : 'default'}
                            onClick={() => {
                                setActiveButton('dislike')
                                write_to_log(`${user.name} disliked the following message: ${content}`)
                            }}
                        >
                            <ThumbDownOffAltIcon fontSize="small"/>
                        </IconButton>
                        <Typography variant="body2">No</Typography>
                    </Box>
                </Box>
            }
        </Box>
    );
};

export default Message;