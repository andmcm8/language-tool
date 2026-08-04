export interface StoreHours {
  monday_friday: string;
  saturday: string;
  sunday: string;
}

export interface StorePolicies {
  restroomLocationEs?: string;
  restroomLocationEn?: string;
  restroomCodeEs?: string;
  restroomCodeEn?: string;
  wifiName?: string;
  wifiPassword?: string;
  parkingPolicyEs?: string;
  parkingPolicyEn?: string;
  ebtPolicyEs?: string;
  ebtPolicyEn?: string;
  returnPolicyEs?: string;
  returnPolicyEn?: string;
  deliveryPolicyEs?: string;
  deliveryPolicyEn?: string;
}

export interface StoreInfo {
  id: string;
  name: string;
  tagline: string;
  address: string;
  phone: string;
  email?: string;
  hours: StoreHours;
  paymentMethods: string[];
  amenities: string[];
  themeColor?: string;
  logoIcon?: string;
  policies?: StorePolicies;
}

export interface Category {
  id: string;
  nameEs: string;
  nameEn: string;
  icon?: string;
  descriptionEs?: string;
  descriptionEn?: string;
}

export interface Product {
  id: string;
  categoryId: string;
  nameEs: string;
  nameEn: string;
  descriptionEs: string;
  descriptionEn: string;
  price: string;
  ingredientsEs?: string;
  ingredientsEn?: string;
  priceSubtextEs?: string;
  priceSubtextEn?: string;
  image?: string;
  popular?: boolean;
  badge?: string;
  allergens?: string[];
  tags?: string[];
  ctaType?: "in_store" | "phone" | "custom";
}

export interface Faq {
  qEs: string;
  qEn: string;
  aEs: string;
  aEn: string;
}

export interface MerchantConfig {
  storeInfo: StoreInfo;
  categories: Category[];
  products: Product[];
  faqs: Faq[];
}
