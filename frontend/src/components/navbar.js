import React from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';

export default function NavBar() {
  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
      <Container>
        <Link to='/' className='me-4' style={{textDecoration: 'none', color: 'white', fontSize: '20px'}}>Product Hunt</Link>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Link to='/about' style={{textDecoration: 'none', color: 'white'}}>About</Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}