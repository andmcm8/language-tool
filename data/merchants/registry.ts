import { MerchantConfig } from '@/types/merchant';
import bedford_thai from './bedford-thai.json';
import clover_pharmacy from './clover-pharmacy.json';
import demo from './demo.json';
import elsol from './elsol.json';
import honey_joes_family_coffeehouse from './honey-joes-family-coffeehouse.json';
import hudson_social from './hudson-social.json';
import le_pain_quotidien from './le-pain-quotidien.json';
import mr_falafel from './mr-falafel.json';
import stamford_repairs from './stamford-repairs.json';

export const MERCHANTS_REGISTRY: Record<string, MerchantConfig> = {
  'bedford-thai': bedford_thai as unknown as MerchantConfig,
  'clover-pharmacy': clover_pharmacy as unknown as MerchantConfig,
  'demo': demo as unknown as MerchantConfig,
  'elsol': elsol as unknown as MerchantConfig,
  'honey-joes-family-coffeehouse': honey_joes_family_coffeehouse as unknown as MerchantConfig,
  'hudson-social': hudson_social as unknown as MerchantConfig,
  'le-pain-quotidien': le_pain_quotidien as unknown as MerchantConfig,
  'mr-falafel': mr_falafel as unknown as MerchantConfig,
  'stamford-repairs': stamford_repairs as unknown as MerchantConfig,
};
