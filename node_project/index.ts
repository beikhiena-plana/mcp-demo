import 'dotenv/config';

import express from 'express';
import logger from './logger';
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';

const app = express();
const port = process.env.PORT || 3000;

// Swagger Configuration
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'TekTok Demo API',
      version: '1.0.0',
      description: 'API Documentation for MCP Logging Demo project',
    },
    servers: [{ url: `http://localhost:${port}` }],
  },
  apis: ['./index.ts'], // Points to JSDoc comments in this file
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);

// Json Middleware
app.use(express.json());

// Log every incoming request for MCP visibility
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.url}`);
  next();
});

// ROUTES

// Swagger UI Route
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

/**
 * @openapi
 * /error:
 *   get:
 *     summary: Trigger a test error
 *     description: Forces a failure for MCP debugging.
 *     responses:
 *       500:
 *         description: Internal Server Error
 */
app.get('/error', (req, res) => {
  try {
    const userData: any = null; 
    return res.status(200).json({ name: userData.name });
  } catch (err) {
    logger.error(err); // Logs stack trace to error.log for MCP to find
    res.status(500).send("Internal Server Error");
  }
});

// Start Server
app.listen(port, () => {
  logger.info(`Server is running at http://localhost:${port}`);
  logger.info(`Swagger docs available at http://localhost:${port}/api-docs`);
});
