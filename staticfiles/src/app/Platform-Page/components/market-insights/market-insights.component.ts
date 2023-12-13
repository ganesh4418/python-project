import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/shared/user-service.service';

@Component({
  selector: 'app-market-insights',
  templateUrl: './market-insights.component.html',
  styleUrls: ['./market-insights.component.css']
})
export class MarketInsightsComponent {

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
    this.userService.isUserLoggedIn$.subscribe((res) => {
      if (!res) {
        this.router.navigate([""]);
        return;
      }
    });
  }

}