import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  /** Base URL of the FastAPI backend */
  private readonly BASE_URL = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  // ── Helpers ──────────────────────────────────────────────────────────────

  /** Build auth headers from the JWT stored in localStorage */
  private authHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    });
  }

  // ── Auth ─────────────────────────────────────────────────────────────────

  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.BASE_URL}/auth/login`, { email, password });
  }

  // ── Usuarios ─────────────────────────────────────────────────────────────

  getUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/usuarios`, {
      headers: this.authHeaders(),
    });
  }

  createUsuario(data: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/usuarios`, data, {
      headers: this.authHeaders(),
    });
  }

  // ── Empresas ─────────────────────────────────────────────────────────────

  getEmpresas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/empresas`, {
      headers: this.authHeaders(),
    });
  }

  createEmpresa(data: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/empresas`, data, {
      headers: this.authHeaders(),
    });
  }

  // ── Sucursales ────────────────────────────────────────────────────────────

  getSucursales(): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/sucursales`, {
      headers: this.authHeaders(),
    });
  }

  createSucursal(data: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/sucursales`, data, {
      headers: this.authHeaders(),
    });
  }

  // ── Generic (use for any other endpoint) ────────────────────────────────

  get<T>(path: string): Observable<T> {
    return this.http.get<T>(`${this.BASE_URL}${path}`, {
      headers: this.authHeaders(),
    });
  }

  post<T>(path: string, body: any): Observable<T> {
    return this.http.post<T>(`${this.BASE_URL}${path}`, body, {
      headers: this.authHeaders(),
    });
  }

  put<T>(path: string, body: any): Observable<T> {
    return this.http.put<T>(`${this.BASE_URL}${path}`, body, {
      headers: this.authHeaders(),
    });
  }

  delete<T>(path: string): Observable<T> {
    return this.http.delete<T>(`${this.BASE_URL}${path}`, {
      headers: this.authHeaders(),
    });
  }
}
