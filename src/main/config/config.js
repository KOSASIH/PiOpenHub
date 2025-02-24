// src/main/config/config.js

const dotenv = require('dotenv');
const Joi = require('joi');

// Load environment variables from .env file
dotenv.config();

// Define a schema for validating environment variables
const schema = Joi.object({
    NODE_ENV: Joi.string().valid('development', 'testing', 'production').default('development'),
    PORT: Joi.number().default(3000),
    DATABASE_URL: Joi.string().uri().required(),
    API_KEY: Joi.string().required(),
    SECRET_KEY: Joi.string().min(32).required(),
    LOG_LEVEL: Joi.string().valid('error', 'warn', 'info', 'debug').default('info'),
    JWT_EXPIRATION: Joi.string().default('1h'),
    REDIS_URL: Joi.string().uri().optional(),
    ENABLE_CORS: Joi.boolean().default(true),
}).unknown(); // Allow unknown keys

// Validate the environment variables
const { error, value: validatedEnv } = schema.validate(process.env);

if (error) {
    throw new Error(`Config validation error: ${error.message}`);
}

// Export the validated configuration
const config = {
    environment: validatedEnv.NODE_ENV,
    port: validatedEnv.PORT,
    databaseUrl: validatedEnv.DATABASE_URL,
    apiKey: validatedEnv.API_KEY,
    secretKey: validatedEnv.SECRET_KEY,
    logLevel: validatedEnv.LOG_LEVEL,
    jwtExpiration: validatedEnv.JWT_EXPIRATION,
    redisUrl: validatedEnv.REDIS_URL,
    enableCors: validatedEnv.ENABLE_CORS,
};

module.exports = config;
