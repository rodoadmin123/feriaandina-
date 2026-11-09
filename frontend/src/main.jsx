import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import { CarritoProveedor } from "./dominios/pedidos/CarritoContexto.jsx";
import "./estilos.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      {/* El carrito se comparte entre todas las pantallas */}
      <CarritoProveedor>
        <App />
      </CarritoProveedor>
    </BrowserRouter>
  </React.StrictMode>
);
