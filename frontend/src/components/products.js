import React from 'react';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';
import Badge from 'react-bootstrap/Badge';

export default function Products(props) {
    const handleLink = (url) => {
        window.open(url, '_blank').focus();
    }

    return (
        <div className='container my-3'>
            {props.products.length === 0 ? <h1>No Products Found!</h1> :
                <Row sm={1} md={2} lg={3} xl={4} xxl={4} className="g-4">
                    {props.products.map(product =>
                        <Col className='p-1'>
                            <Card className='d-block mx-auto' style={{ height: '489px', width: '300px', border: '1px solid' }}>
                                <Card.Img variant="top" className='d-block mx-auto' src={product.image} alt='No Image Found' style={{
                                    width: '235px', height: '230px', borderRadius: '10px' }} />
                                <Card.Body>
                                    <Card.Title className='text-center' style={{ height: '80px', fontSize: '20px' }}>{product.name.length >= 75 ? product.name.slice(0, 75) + "..." : product.name}</Card.Title>
                                </Card.Body>
                                <ListGroup className="list-group-flush">
                                    <ListGroup.Item className='text-center' style={{ fontWeight: 'bold' }}>Rs. {product.price}</ListGroup.Item>
                                    <ListGroup.Item className='text-center'>Rating: {product.rating} and Reviews {product.reviews}</ListGroup.Item>
                                </ListGroup>
                                <Card.Body className='p-2'>
                                    <div className="d-flex justify-content-center align-items-center">
                                        <Button className='me-3' variant="dark" onClick={() => handleLink(product.url)}>Purchase</Button>
                                        <Badge pill bg="secondary">{product.site}</Badge>
                                    </div>
                                </Card.Body>
                            </Card>
                        </Col>
                    )}
                </Row>
            }
        </div>
    );
}
