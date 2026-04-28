import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { ButtonComponent } from '../button/button';

@Component({
  selector: 'app-hero-home',
  imports: [ButtonComponent],
  templateUrl: './hero-home.html',
  styleUrl: './hero-home.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class HeroHome {}
