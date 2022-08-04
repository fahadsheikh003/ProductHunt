import React from 'react';

export default function About() {
  const containerStyle = {
    height: '85.75vh'
  }
  return (
    <div className='container d-flex flex-column justify-content-center' style={containerStyle}>
      <h1 className='text-center'>
        About Us
      </h1>
      <h2><center>This is site searches for best ranked products on <b>Amazon</b>, <b>Aliexpress</b>, <b>Flipkart</b>, <b>Daraz</b>, and <b>Ebay</b>.</center></h2>
      <h3><center>Site developed by <span style={{fontFamily: 'Dancing Script'}}>DEvil</span></center></h3>
    </div>
  )
}
