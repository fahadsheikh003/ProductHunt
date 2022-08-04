import React, { useState } from 'react';
import Search from './components/search';
import Navbar from './components/navbar';
import Footer from './components/footer';
import About from './components/about';
import Products from './components/products';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import LoadingBar from 'react-top-loading-bar';

function App() {
  const [products, setProducts] = useState([])
  const [progress, setProgress] = useState(0)
  
  return (
    <BrowserRouter>
      <LoadingBar color="#f11946" progress={progress} onLoaderFinished={() => setProgress(0)} />
      <Navbar />
      <Routes>
        <Route exact path='/' element={<Search setProducts={setProducts} setProgress={setProgress} />} />
        <Route exact path='/search' element={<Search setProducts={setProducts} setProgress={setProgress} />} />
        <Route exact path='/home' element={<Search setProducts={setProducts} setProgress={setProgress} />} />
        <Route exact path='/result' element={<Products products={products} />} />
        <Route exact path='/about' element={<About />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
