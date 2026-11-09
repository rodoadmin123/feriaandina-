import { Route, Routes } from "react-router-dom";
import BarraNavegacion from "./compartido/componentes/BarraNavegacion.jsx";
import Catalogo from "./dominios/catalogo/paginas/Catalogo.jsx";
import DetalleProducto from "./dominios/catalogo/paginas/DetalleProducto.jsx";
import PublicarProducto from "./dominios/artesanos/paginas/PublicarProducto.jsx";
import Carrito from "./dominios/pedidos/paginas/Carrito.jsx";

// Rutas = pantallas. Cada pantalla pertenece a un contexto del dominio.
export default function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Catalogo />} />                       {/* Catalogo */}
        <Route path="/producto/:id" element={<DetalleProducto />} />    {/* Catalogo */}
        <Route path="/vender" element={<PublicarProducto />} />         {/* Artesanos */}
        <Route path="/carrito" element={<Carrito />} />                 {/* Pedidos */}
      </Routes>
      <BarraNavegacion />
    </div>
  );
}
