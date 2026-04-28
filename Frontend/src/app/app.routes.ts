import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { CreateUser } from './pages/create-user/create-user';
import { CreateCompany } from './pages/create-company/create-company';
import { CreateBranch } from './pages/create-branch/create-branch';
import { SidebarLayout } from './components/sidebar/sidebar';
import { SiteSidebar } from './pages/site-sidebar/site-sidebar';
import { Administracion } from './pages/on-site/administracion/administracion';
import { Nopage } from './pages/on-site/nopage/nopage';
import { Overview } from './pages/on-site/overview/overview';
import { NewRequests } from './pages/on-site/new-requests/new-requests';
import { Workers } from './pages/on-site/workers/workers';
import { NewUserForm } from './components/new-user-form/new-user-form';
import { Vehicles } from './pages/on-site/vehicles/vehicles';
import { NewBranchForm } from './components/new-branch-form/new-branch-form';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'new-branch-form', component: NewBranchForm },
  { path: 'login', component: Login },
  { path: 'home', component: Home },
  { path: 'new-user-form', component: NewUserForm },
  {
    path: '',
    component: SidebarLayout,
    children: [
      { path: 'create-user', component: CreateUser },
      { path: 'create-company', component: CreateCompany },
      { path: 'create-branch', component: CreateBranch },
    ],
  },
  {
    path: 'site-view',
    component: SiteSidebar,
    canActivate: [AuthGuard],
    children: [
      { path: 'admin', component: Administracion },
      { path: 'vehicles', component: Vehicles },
      { path: 'new-requests', component: NewRequests },
      { path: 'overview', component: Overview },
      { path: 'workers', component: Workers },
      { path: '**', component: Nopage },
    ],
  },
];
