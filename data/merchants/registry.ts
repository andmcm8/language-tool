import { MerchantConfig } from '@/types/merchant';
import arezzo from './arezzo.json';
import bartaco from './bartaco.json';
import bedford_thai from './bedford-thai.json';
import clover_pharmacy from './clover-pharmacy.json';
import coffee_an_donut_shop from './coffee-an-donut-shop.json';
import demo from './demo.json';
import elsol from './elsol.json';
import heibecks_stand from './heibecks-stand.json';
import honey_joes_family_coffeehouse from './honey-joes-family-coffeehouse.json';
import hudson_social from './hudson-social.json';
import le_pain_quotidien from './le-pain-quotidien.json';
import mr_falafel from './mr-falafel.json';
import oko from './oko.json';
import rizzutos_oyster_bar_restaurant from './rizzutos-oyster-bar-restaurant.json';
import sherwood_diner from './sherwood-diner.json';
import stamford_repairs from './stamford-repairs.json';
import the_granola_bar from './the-granola-bar.json';
import viva_zapata from './viva-zapata.json';
import winfield_street_coffee from './winfield-street-coffee.json';

export const MERCHANTS_REGISTRY: Record<string, MerchantConfig> = {
  'arezzo': arezzo as unknown as MerchantConfig,
  'bartaco': bartaco as unknown as MerchantConfig,
  'bedford-thai': bedford_thai as unknown as MerchantConfig,
  'clover-pharmacy': clover_pharmacy as unknown as MerchantConfig,
  'coffee-an-donut-shop': coffee_an_donut_shop as unknown as MerchantConfig,
  'demo': demo as unknown as MerchantConfig,
  'elsol': elsol as unknown as MerchantConfig,
  'heibecks-stand': heibecks_stand as unknown as MerchantConfig,
  'honey-joes-family-coffeehouse': honey_joes_family_coffeehouse as unknown as MerchantConfig,
  'hudson-social': hudson_social as unknown as MerchantConfig,
  'le-pain-quotidien': le_pain_quotidien as unknown as MerchantConfig,
  'mr-falafel': mr_falafel as unknown as MerchantConfig,
  'oko': oko as unknown as MerchantConfig,
  'rizzutos-oyster-bar-restaurant': rizzutos_oyster_bar_restaurant as unknown as MerchantConfig,
  'sherwood-diner': sherwood_diner as unknown as MerchantConfig,
  'stamford-repairs': stamford_repairs as unknown as MerchantConfig,
  'the-granola-bar': the_granola_bar as unknown as MerchantConfig,
  'viva-zapata': viva_zapata as unknown as MerchantConfig,
  'winfield-street-coffee': winfield_street_coffee as unknown as MerchantConfig,
};
