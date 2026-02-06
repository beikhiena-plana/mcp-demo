import winston from 'winston';

const { combine, timestamp, printf, colorize, errors } = winston.format;

// Custom format for readable logs
const logFormat = printf(({ level, message, timestamp, stack }) => {
  return `${timestamp} [${level}]: ${stack || message}`;
});

const logger = winston.createLogger({
  level: 'info',
  format: combine(
    timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    errors({ stack: true }), // This captures the stack trace
    logFormat
  ),
  transports: [
    // 1. Write all errors to error.log
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    // 2. Write everything to combined.log
    new winston.transports.File({ filename: 'logs/combined.log' }),
    // 3. Also log to console with colors
    new winston.transports.Console({
      format: combine(colorize(), logFormat)
    })
  ],
});

export default logger;
