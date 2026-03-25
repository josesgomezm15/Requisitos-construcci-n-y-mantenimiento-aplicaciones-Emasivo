Stack de desarrollo

Componente	Tecnología
backend	Mínimo: Flask WSGI Framework
Esperado: FastAPI web framework
Frontend	Minimo: 
•	Flask HTML Template
•	FastAPI HTML Template
Esperado opcional: VUE
Base de datos	SQL Server 2019 – Mandatorio 
WEB Server	NGINX – Mandatorio 


Arquitectura:

Cómo minimo se debe construir una app Monolitica, pero puede escalar a aplicaciones de mayor arquitectura. A continuación los principales aspectos a tener en cuenta para el desarrollo de la app:

Componente	Directriz 
Patron de diseño	Mínimo: MVC – Documentado el código
Gestión de datos – Documentación 	•	Diagrama de base de datos – Mandatorio - Mínimo
Gestión de datos – Generación base de datos 	•	Script – Mandatorio – Mínimo
•	Migraciones – Esperado
	•	


Seguridad de la información – Gobierno de datos 

Autenticación:

•	Implementar inicio de sesión mediante usuario y contraseña: Longitud mínima de 10 caracteres, composición alfanumérica 
•	Implementar mecanismo de recuperación de credenciales 
•	Implementar mecanismo de cambio de contraseña 

Control de acceso:

•	Implementar roles y permisos, entregando la matriz de segregación 
•	

Administración y soporte

•	La administración de usuarios debe entregarse como un proceso documentado al proceso de tecnología y en adelante será este último el que gestione por mesa de ayuda y control de identidades la gestión de usuarios 
•	El soporte en ambiente productivo debe realizarse por mesa de ayuda, por lo que una vez la app pase a un ambiente productivo, se debe transferir conocimiento al equipo de TIC de mes de ayuda
•	El incremento de capacidades (nuevos desarrollos), debe realizarse por un requerimiento de mesa de ayuda y cursar el proceso de gestión del cambio de tecnología según el SIG

UI/UX

•	La interfaz de usuario debe ser amigable, intuitiva y obedecer a la lógica del flujo de trabajo de la situación o problema que resuelve la app
•	La interfaz debe asegurarse para el tamaño pactado (desktop, laptot, Tablet, etc) y diseño responsivo 
•	Los resultados para mostrar al usuario deben ser paginados del lado del servidor, asegurando consultas eficientes y por ende un rendimiento optimo de la interfaz y experiencia de uso. 

Control de versiones y repositorio.

•	El control de repositorio será github.com, por lo que inicialmente deben tener su cuenta activa
