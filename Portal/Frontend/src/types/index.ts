export interface User {
  user_id: number;
  chart_id: string;
  first_name: string;
  email: string;
  timestamp: string;
  telegram_id: string;
  youtube_id: number;
  insta_id: number;
}

export interface Challenge {
  id: number;
  challenge_name: string;
  task: string;
  links: string;
  taskon: string;
  duration: number;
  prize: string;
  timestamp: string;
  challenge_task: any;
}

export interface Progress {
  id: number;
  user_id: number;
  submit: boolean;
  link: string;
  challenge_day_id: string;
  submition_day: string;
  text: string;
  challenge_name: string;
  day: string;
  challenge_id: number;
}

export interface Winner {
  id: number;
  challenge_id: number;
  user_id: number;
  status: string;
}

export interface Instagram {
  insta_id: number;
  username: string;
  email: string;
  name: string;
  timestamp: string;
  followers: number;
  following: number;
  profile: string;
}

export interface Youtube {
  youtube_id: number;
  channel_name: string;
  subscribers: number;
  timestamp: string;
}