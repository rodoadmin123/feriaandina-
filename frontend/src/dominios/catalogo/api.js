// CONTEXTO CATALOGO: llamadas a la API de Django
import { pedirApi } from "../../compartido/api.js";

export const listarProductos = ({ categoria, texto } = {}) => {
  const params = new URLSearchParams();
  if (categoria) params.set("categoria", categoria);
  if (texto) params.set("q", texto);
  return pedirApi(`/productos/?${params}`);
};
export const obtenerProducto = (id) => pedirApi(`/productos/${id}/`);
export const listarCategorias = () => pedirApi("/categorias/");

// El artesano publica: se envia como FormData porque lleva una FOTO
export const publicarProducto = (formData) =>
  pedirApi("/productos/", { method: "POST", body: formData });
