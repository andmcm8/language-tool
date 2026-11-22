import type { Metadata } from "next";
import LegalPage, { Section } from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Terms of Use — DuoTaps",
  description: "The terms that apply when you use DuoTaps.",
};

const EMAIL = "contact@duotaps.com";

export default function TermsPage() {
  return (
    <LegalPage
      title="Terms of Use"
      updated="November 21, 2026"
      intro={
        <p>
          These terms apply to your use of the DuoTaps website and tools (the &ldquo;Service&rdquo;). By using the Service, you
          agree to them. If you don&rsquo;t agree, please don&rsquo;t use the Service. Our{" "}
          <a href="/privacy" className="font-semibold text-primary">Privacy Policy</a> explains how we handle information.
        </p>
      }
    >
      <Section title="What DuoTaps is">
        <p>DuoTaps is an independent, free guide that shows menus and information for restaurants and other places in English and Spanish, along with translation and assistant tools.</p>
        <p><strong>DuoTaps is not affiliated with, endorsed by, or sponsored by the businesses listed</strong> unless a listing clearly says otherwise. Business names, logos and trademarks belong to their owners and are used only to identify the businesses.</p>
      </Section>

      <Section title="Menu and business information">
        <p>Menus, prices, hours and other details are compiled from publicly available sources and with the help of automated tools, including AI. They may be incomplete, out of date or inaccurate, and they may not match what a business currently offers or charges. <strong>Always confirm details with the business before relying on them.</strong> The business&rsquo;s own menu and prices control.</p>
      </Section>

      <Section title="Allergies and dietary needs">
        <p><strong>Do not rely on DuoTaps for allergy, ingredient, nutrition or dietary information.</strong> We can&rsquo;t confirm how dishes are prepared or whether they contain allergens or have been in contact with them. If you have a food allergy, intolerance or other dietary or health need, ask the restaurant&rsquo;s staff directly before ordering.</p>
      </Section>

      <Section title="AI features and translations">
        <p>The assistant, translator and camera tool use automated and AI technology. Their answers and translations can be wrong or incomplete and are provided for general information only. They are not professional, medical, legal or other advice, and don&rsquo;t speak for any business.</p>
      </Section>

      <Section title="Acceptable use">
        <p>You agree not to:</p>
        <ul>
          <li>use the Service for anything unlawful, harmful or misleading;</li>
          <li>scrape, copy or harvest the Service or its content in bulk, or use automated means to access it in a way that burdens it;</li>
          <li>try to break, overload, probe or bypass the security of the Service;</li>
          <li>submit content that infringes others&rsquo; rights, or that is abusive, hateful or sexually explicit.</li>
        </ul>
      </Section>

      <Section title="Business owners">
        <p>If you own or represent a listed business and want your information corrected or removed, email <a href={`mailto:${EMAIL}`}>{EMAIL}</a> or use the request form on your listing. We review requests promptly and will correct or remove listings at no cost.</p>
      </Section>

      <Section title="Content you send us">
        <p>You keep ownership of what you send us. You give us permission to use it as needed to operate and improve the Service, for example to answer a question or update a menu you&rsquo;ve sent us.</p>
      </Section>

      <Section title="Our content">
        <p>The DuoTaps name, design, software and original content are owned by DuoTaps and protected by law. You may use the Service for your own personal, non-commercial purposes.</p>
      </Section>

      <Section title="Links to other sites">
        <p>The Service may link to other websites, such as maps or a business&rsquo;s own site. We don&rsquo;t control them and aren&rsquo;t responsible for their content or practices.</p>
      </Section>

      <Section title="Disclaimer">
        <p className="uppercase">The Service is provided &ldquo;as is&rdquo; and &ldquo;as available,&rdquo; without warranties of any kind, express or implied, including warranties of accuracy, merchantability, fitness for a particular purpose and non-infringement. We don&rsquo;t warrant that the Service or its information will be accurate, complete, current, uninterrupted or error-free.</p>
      </Section>

      <Section title="Limitation of liability">
        <p className="uppercase">To the fullest extent permitted by law, DuoTaps will not be liable for any indirect, incidental, special, consequential or punitive damages, or for any loss arising from your use of or reliance on the Service, including information about menus, prices, ingredients or allergens. Our total liability for any claim relating to the Service is limited to $100.</p>
        <p>Some places don&rsquo;t allow these limits, so they may not fully apply to you.</p>
      </Section>

      <Section title="Indemnity">
        <p>You agree to defend and hold DuoTaps harmless from claims arising from your misuse of the Service or your violation of these terms.</p>
      </Section>

      <Section title="Changes and termination">
        <p>We may change, suspend or stop the Service, or update these terms, at any time. If we update the terms, we&rsquo;ll change the &ldquo;Last updated&rdquo; date above. Continuing to use the Service after a change means you accept the updated terms.</p>
      </Section>

      <Section title="Governing law">
        <p>These terms are governed by the laws of the State of Connecticut, without regard to its conflict-of-law rules. Any dispute will be handled in the state or federal courts located in Connecticut.</p>
      </Section>

      <Section title="Contact">
        <p>Questions about these terms: <a href={`mailto:${EMAIL}`}>{EMAIL}</a>.</p>
      </Section>
    </LegalPage>
  );
}
