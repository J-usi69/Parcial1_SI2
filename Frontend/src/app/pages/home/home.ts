import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HeroHome } from '../../components/hero-home/hero-home';
import { GridColumn } from '../../components/grid-column/grid-column';
import { Header } from '../../components/header/header';

@Component({
  selector: 'app-home',
  imports: [HeroHome, GridColumn, Header],
  templateUrl: './home.html',
  styleUrl: './home.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class Home {}
