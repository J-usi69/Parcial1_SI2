import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { ButtonComponent } from '../../components/button/button';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, RouterModule, ButtonComponent],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {
  errorMessage = '';
  isLoading = false;

  constructor(
    private api: ApiService,
    private authService: AuthService,
    private router: Router,
  ) {}

  ngOnInit() {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/site-view/overview']);
    }
  }

  login(email: string, password: string) {
    this.errorMessage = '';

    if (!email || !password) {
      this.errorMessage = 'El correo electrónico y la contraseña son obligatorios.';
      return;
    }

    this.isLoading = true;
    this.api.login(email, password).subscribe({
      next: (response) => {
        localStorage.setItem('access_token', response.access_token);
        this.router.navigate(['/site-view/overview']);
      },
      error: (error) => {
        this.isLoading = false;
        if (error?.status === 401) {
          this.errorMessage = 'Correo o contraseña inválidos.';
        } else {
          this.errorMessage = 'No se pudo iniciar sesión. Intenta de nuevo.';
        }
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }
}
