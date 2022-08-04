import axios from 'axios';
import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from 'react-router-dom';

export default function Search(props) {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const handleQuery = () => {
    if (query === "")
      return;
    const encodedQuery = encodeURI(query);

    const timeOuts = [];
    for (let i = 1; i<=30; i++) {
      timeOuts.push(setTimeout(()=>{
        props.setProgress(i*2)
      }, i*1000));
    }

    const fetchData = async () => {
      let { data } = await axios.get('/search?query=' + encodedQuery);
      
      timeOuts.forEach((timeOut) => {
        clearTimeout(timeOut)
      })
      props.setProgress(100)
      
      if (data['status'] === 'success') {
        props.setProducts(data['data']);
        navigate('/result')
      }
    }
    fetchData();
  }

  const titleStyle = {
    fontFamily: 'Dancing Script'
  }

  const containerStyle = {
    height: '85.75vh'
  }

  return (
    <div className="d-flex flex-column justify-content-center align-items-center" style={containerStyle}>
      <h1 className="mb-5 display-1" style={titleStyle}>Product Hunt</h1>
        <Form.Control
          type="search"
          placeholder="Search"
          aria-label="Search"
          className='w-75'
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <Button className="my-3" variant="outline-dark" onClick={handleQuery}>Search</Button>
    </div>
  );
}
