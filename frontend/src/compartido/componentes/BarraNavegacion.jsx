import { NavLink } from "react-router-dom";
import { useCarrito } from "../../dominios/pedidos/CarritoContexto.jsx";
import Icono from "./Icono.jsx";

// Barra inferior: queda en la "zona del pulgar" para usar con una mano.
export default function BarraNavegacion() {
  const { cantidadTotal } = useCarrito();
  return (
    <nav className="barra-nav" aria-label="Navegación principal">
      <NavLink to="/" end className="nav-item">
        <Icono nombre="tienda" />
        <span>Catálogo</span>
      </NavLink>
      <NavLink to="/vender" className="nav-item nav-vender">
        <span className="nav-vender-circulo"><Icono nombre="camara" /></span>
        <span>Vender</span>
      </NavLink>
      <NavLink to="/carrito" className="nav-item">
        <span className="nav-icono-badge">
          <Icono nombre="carrito" />
          {cantidadTotal > 0 && <b className="badge">{cantidadTotal}</b>}
        </span>
        <span>Carrito</span>
      </NavLink>
    </nav>
  );
}
