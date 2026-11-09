import { Link } from "react-router-dom";
import { soles } from "../../../compartido/api.js";

// Componente reutilizable (principio de reutilizacion del IDL1):
// se usa en el catalogo y podria usarse en "recomendados".
export default function TarjetaProducto({ producto }) {
  return (
    <Link to={`/producto/${producto.id}`} className="tarjeta">
      <img src={producto.foto_url} alt={producto.nombre} loading="lazy" />
      <div className="tarjeta-cuerpo">
        <h3>{producto.nombre}</h3>
        <p className="tarjeta-origen">{producto.artesano.comunidad}</p>
        <p className="precio">{soles(producto.precio)}</p>
      </div>
    </Link>
  );
}
