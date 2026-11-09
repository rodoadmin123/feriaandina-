import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { soles } from "../../../compartido/api.js";
import Contador from "../../../compartido/componentes/Contador.jsx";
import Icono from "../../../compartido/componentes/Icono.jsx";
import { useCarrito } from "../../pedidos/CarritoContexto.jsx";
import { obtenerProducto } from "../api.js";

// PANTALLA 2 - DETALLE DEL PRODUCTO (IDL1, paso 5: agregar al carrito)
export default function DetalleProducto() {
  const { id } = useParams();
  const navegar = useNavigate();
  const { agregar } = useCarrito();
  const [producto, setProducto] = useState(null);
  const [cantidad, setCantidad] = useState(1);
  const [error, setError] = useState("");

  useEffect(() => {
    obtenerProducto(id).then(setProducto).catch((e) => setError(e.message));
  }, [id]);

  if (error) return <main className="pantalla"><p className="aviso aviso-error">{error}</p></main>;
  if (!producto) return <main className="pantalla"><p className="vacio">Cargando…</p></main>;

  const alAgregar = () => {
    agregar(producto, cantidad);
    navegar("/carrito");
  };

  return (
    <main className="pantalla pantalla-con-accion">
      <div className="detalle-foto">
        <button className="boton-flotante" onClick={() => navegar(-1)} aria-label="Volver">
          <Icono nombre="atras" />
        </button>
        <img src={producto.foto_url} alt={producto.nombre} />
      </div>
      <section className="detalle-info">
        <h1>{producto.nombre}</h1>
        <p className="precio precio-grande">{soles(producto.precio)}</p>
        <div className="artesano-ficha">
          <span className="avatar">{producto.artesano.nombre[0]}</span>
          <div>
            <strong>{producto.artesano.nombre}</strong>
            <span><Icono nombre="ubicacion" tam={14} /> {producto.artesano.comunidad}, Junín</span>
          </div>
        </div>
        <p className="descripcion">{producto.descripcion}</p>
        <div className="fila-cantidad">
          <div>
            <strong>Cantidad</strong>
            <span className="stock">Quedan {producto.stock}</span>
          </div>
          <Contador valor={cantidad} onCambiar={setCantidad} maximo={producto.stock} etiqueta="Cantidad" />
        </div>
      </section>
      <div className="accion-fija">
        <button className="boton-principal" onClick={alAgregar}>
          Agregar al carrito · {soles(producto.precio * cantidad)}
        </button>
      </div>
    </main>
  );
}
