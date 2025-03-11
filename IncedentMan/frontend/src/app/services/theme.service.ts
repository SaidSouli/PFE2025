import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private isDarkModeSubject = new BehaviorSubject<boolean>(false);
  isDarkMode$ = this.isDarkModeSubject.asObservable();

  constructor() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      this.isDarkModeSubject.next(savedTheme === 'dark');
    }
  }

  toggleDarkMode(): void {
    const newMode = !this.isDarkModeSubject.value;
    this.isDarkModeSubject.next(newMode);
    localStorage.setItem('theme', newMode ? 'dark' : 'light');
  }

  getCurrentTheme(): boolean {
    return this.isDarkModeSubject.value;
  }
}