# AI Development Guide

This document provides guidance for AI developers working on the Travel Agent Assistant project.

## Project Overview

The goal of this project is to create an AI-powered application that helps travel agents find the best travel options for their clients. The application should consider factors like visa requirements, budget, and travel preferences to provide intelligent recommendations.

## Core APIs

* **Amadeus for Developers:**
    * Flight Offers Search
    * Airport & City Search
    * Hotel Search
    * Airport Nearest Relevant
* **External Visa Service:** (To be determined)

## Development Guidelines

* **Backend:** The backend is built with Python and Flask. All API interactions should be handled by the backend.
* **Frontend:** The frontend is a simple HTML, CSS, and JavaScript application. The frontend should be used to gather user input and display the results from the backend.
* **AI Logic:** The core AI logic for routing and recommendations should be implemented in the backend. This will involve:
    * Calling the Amadeus APIs to get flight, hotel, and other travel data.
    * Integrating with a visa service to get visa requirements for different countries.
    * Implementing algorithms to find the best travel routes based on the user's criteria.
* **Code Style:** Please follow standard Python and JavaScript code style guidelines.
* **Testing:** Please write unit tests for all new backend functionality.
* **Dependencies:** Add any new dependencies on `backend/requirements.txt`.
