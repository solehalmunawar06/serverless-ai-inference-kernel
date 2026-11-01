# System Architecture

## 1. Overview

Serverless AI Inference Execution Kernel adalah application-level OS kernel yang dirancang untuk menjalankan fungsi AI/inference secara cepat dan terisolasi.

Sistem menyediakan REST API menggunakan FastAPI sebagai interface antara client dan execution kernel.

## 2. Architecture Components

### Client

Client mengirimkan request inference melalui REST API.

### FastAPI API

FastAPI menerima request pada endpoint `/inference`, melakukan validasi input, dan meneruskan request ke execution layer.

### Function Registry

Function Registry menyimpan daftar fungsi AI yang tersedia dan dapat dipanggil secara dinamis berdasarkan nama fungsi pada request.

### Execution Kernel

Execution Kernel menjalankan fungsi yang dipilih, mengukur waktu eksekusi, dan menghasilkan response.

### Response

Hasil eksekusi dikembalikan kepada client dalam format JSON.

## 3. Execution Flow

```text
Client
   |
   v
POST /inference
   |
   v
Request Validation
   |
   v
Function Registry
   |
   v
Execution Kernel
   |
   +----> AI Function
   |
   v
Execution Time Measurement
   |
   v
JSON Response
