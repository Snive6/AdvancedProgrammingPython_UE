import {
  Box,
  Button,
  MenuItem,
  Select,
  SelectChangeEvent,
  TextField,
  Typography,
} from '@mui/material';
import { MainContainer } from '../components';
import { useState } from 'react';
import axios from 'axios';
import { ApiUrlAdres, SumarizedModels } from '../types';
import { useAuth } from '../hooks';
import React from 'react';

export default function SummaryPage() {
  const [sumarizedText, setSumarizedText] = useState('');
  const { token } = useAuth();
  const [model, setModel] = React.useState<SumarizedModels>(
    SumarizedModels.extractive_summarizer,
  );

  const handleChange = (event: SelectChangeEvent) => {
    setModel(event.target.value as SumarizedModels);
  };

  const handleClick = () => {
    if (token) {
      axios.get(`${ApiUrlAdres}/summarize`).then((response) => {
        console.log(response);
        setSumarizedText(response.data as string);
      });
    } else {
      axios.get(`${ApiUrlAdres}/summarize`).then((response) => {
        console.log(response);
        setSumarizedText(response.data as string);
      });
    }
  };

  return (
    <MainContainer>
      <TextField
        id="outlined-sumarized-text"
        label="Sumarized text"
        variant="outlined"
        multiline
        rows={20}
        sx={{ marginTop: 2 }}
        fullWidth
      />
      <Box sx={{ margin: 3, justifyContent: 'center', spaces: 10 }}>
        <Select
          sx={{ width: '300px' }}
          label="Model type"
          onChange={handleChange}
          value={model}
        >
          {Object.values(SumarizedModels).map((value) => {
            return <MenuItem value={value}>{value}</MenuItem>;
          })}
        </Select>
        <Button id="outlined" variant="outlined" onClick={handleClick}>
          Submit
        </Button>
      </Box>
      <Typography>{sumarizedText}</Typography>
    </MainContainer>
  );
}
