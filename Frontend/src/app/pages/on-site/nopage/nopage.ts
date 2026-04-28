import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [RouterLink],
  template: `
    <div class="min-h-screen bg-gray-950 flex items-center justify-center p-6 text-center">
      <div class="max-w-md">
        <h1 class="text-9xl font-black text-white opacity-10">404</h1>
        <h2 class="text-3xl font-bold text-white mt-4">Página no encontrada</h2>
        <p class="text-gray-400 mt-4 mb-8">
          Lo sentimos, la página que buscas parece haber sido movida o no existe.
        </p>
        <a
          routerLink="/home"
          class="inline-block bg-indigo-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-indigo-700 transition-all"
        >
          Volver al inicio
        </a>
      </div>
    </div>
  `,
})
export class Nopage {}
