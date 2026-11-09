// Cliente HTTP compartido: todas las llamadas a Django pasan por aqui.
// Si el back-end responde con error de dominio ({"error": "..."}),
// lo convertimos en una excepcion con un mensaje claro para el usuario.
export async function pedirApi(ruta, opciones = {}) {
  const respuesta = await fetch(`/api${ruta}`, opciones);
  const datos = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) {
    throw new Error(datos.error || "No se pudo conectar con FeriaAndina.");
  }
  return datos;
}

// Formatea montos como en el Peru: S/ 1,250.00
export const soles = (monto) =>
  "S/ " + Number(monto).toLocaleString("es-PE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
