import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { PlatformService } from 'src/app/shared/api-serviceEndpoint/platform.service';
import { UserService } from 'src/app/shared/user-service.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  highlightMenu: any = { 'border-bottom': '1px solid white' };
  home_style: any = this.highlightMenu;
  about_style: any = "";
  research_style: any = "";
  menu_style: any = "";
  isUserLoggedIn: boolean = false;
  loggedInUserName: string = "";
  mainMenuClicked: boolean = false;
  isMenuOpen = false;

  researchMenuInvokedSubscription: Subscription | undefined;
  isUserLoginSubscription: Subscription | undefined;
  getUserProfileImg:string='';

  constructor(private userService: UserService, private router: Router,private platformService:PlatformService) {
  }

  ngOnInit() {
    this.isUserLoginSubscription = this.userService.isUserLoggedIn$.subscribe(res => {
      this.isUserLoggedIn = res;
      this.userLogin();      
    });

    if (location.href.split("#/").length == 1)
      location.replace(location.href + '#/');

    this.menuClicked(location.href.split("#/")[1]);

    this.mainMenuClicked = false;
  }

  userLogin() {
    this.researchMenuInvokedSubscription = this.userService.researchMenuInvoked$.subscribe(res => {
      if (res) {
        this.loggedInUserName = this.userService.userLoginData.first_name + " " + this.userService.userLoginData.last_name;
        this.mainMenuClicked = true;
        this.menuClicked("research");
        this.getProfileImage();
      }
    });
  }

  menuClicked(type?: string) {
    this.home_style = {};
    this.research_style = {};
    this.menu_style = {};
    this.about_style = {};

    switch (type) {
      case "home":
      case "": {
        this.home_style = this.highlightMenu;
        break;
      }
      case "about": {
        this.about_style = this.highlightMenu;
        break;
      }
      case "research": {
        this.research_style = this.highlightMenu;
        break;
      }
      case "marketInsights": {
        this.menu_style = this.highlightMenu;
        break;
      }
    }
  }

  homeRedirect() {
    this.router.navigate([""]);
  }

  userProfile() {
    this.userService.isUserProfileClicked = true;
    this.router.navigate(["platform"]);
  }

  logout() {
    this.researchMenuInvokedSubscription!.unsubscribe();
    this.mainMenuClicked = false;
    this.isUserLoggedIn = false;
    this.loggedInUserName = "";
    this.isMenuOpen = false;
    this.menuClicked("");
    this.router.navigate(["home"]);
  }

  profileRedirect() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  getProfileImage(){
    const user_id = this.userService.userLoginData.user_id;

    this.platformService.getProfileImage(user_id).subscribe((img=>{
      this.getUserProfileImg = img.profile_photo
    }))
  }
}
