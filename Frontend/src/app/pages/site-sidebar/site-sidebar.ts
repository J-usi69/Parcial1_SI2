import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-site-sidebar',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './site-sidebar.html',
  styleUrl: './site-sidebar.css',
})
export class SiteSidebar {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
