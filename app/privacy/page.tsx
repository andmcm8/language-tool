import type { Metadata } from "next";
import LegalPage, { Section } from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Privacy Policy — DuoTaps",
  description: "How DuoTaps collects, uses and protects information.",
};

const EMAIL = "contact@duotaps.com";

export default function PrivacyPage() {
  return (
    <LegalPage
      title="Privacy Policy"
      updated="November 21, 2026"
      intro={
        <p>
          This policy explains what information DuoTaps (&ldquo;DuoTaps,&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;) collects when
          you use our website and tools (the &ldquo;Service&rdquo;), how we use it, and the choices you have. You don&rsquo;t need
          an account to use DuoTaps, and we try to collect as little as possible.
        </p>
      }
    >
      <Section title="Information we collect">
        <p><strong>Information you give us.</strong> If you use a contact form or email us, we receive what you send, such as your email address or phone number, the business you&rsquo;re writing about, and your message.</p>
        <p><strong>Content you submit to our tools.</strong> When you use the assistant, the translator or the camera tool, we process the text you type and the photos you take or upload so we can return an answer or translation. Voice input uses your browser&rsquo;s built-in speech recognition, which is provided by your browser or device maker (for example Google or Apple) under their own privacy terms; we receive only the resulting text.</p>
        <p><strong>Usage information.</strong> We use Vercel Web Analytics to understand overall traffic, such as pages viewed, referring sites, approximate country, and device or browser type. It does not use cookies and does not identify you personally. Like most websites, our hosting provider also keeps short-lived technical logs (such as IP address and browser type) for security and troubleshooting.</p>
        <p><strong>Information stored on your device.</strong> Your assistant conversation and language choice may be saved in your browser&rsquo;s local storage so they&rsquo;re there when you come back. This stays on your device, and you can clear it at any time using the clear-chat option or your browser settings.</p>
      </Section>

      <Section title="How we use information">
        <ul>
          <li>To provide and operate the Service, including answering questions and translating text and photos.</li>
          <li>To respond to messages, including correction and removal requests from business owners.</li>
          <li>To understand how the Service is used in aggregate and improve it.</li>
          <li>To keep the Service secure, prevent abuse, and comply with the law.</li>
        </ul>
      </Section>

      <Section title="How we share information">
        <p><strong>We do not sell or rent your personal information, and we do not share it for targeted advertising.</strong> We keep the information we collect confidential and do not publish or disclose it to third parties, except in these limited cases:</p>
        <ul>
          <li><strong>Service providers</strong> that run the Service for us, only as needed to provide it. These include Vercel (hosting and analytics) and Google (AI and translation services that process assistant messages, translations and photos). Content sent to these providers is handled under their terms, so please don&rsquo;t include sensitive personal information in chats or photos.</li>
          <li><strong>Legal reasons</strong>, if we&rsquo;re required to by law or legal process, or need to protect the rights, safety or property of our users, the public or DuoTaps.</li>
          <li><strong>Business changes</strong>, such as a merger or transfer of the Service, in which case this policy will continue to apply to information collected before the change.</li>
        </ul>
      </Section>

      <Section title="Emails to businesses">
        <p>If we email you about your business&rsquo;s listing, those emails may use standard open and link-click measurement. You can ask us to stop emailing you at any time by replying or writing to <a href={`mailto:${EMAIL}`}>{EMAIL}</a>.</p>
      </Section>

      <Section title="How long we keep information">
        <p>We keep messages you send us for as long as needed to respond and keep a record of the conversation, and delete them on request. Technical logs and analytics are kept only in limited, aggregate or short-term form. We don&rsquo;t keep the photos you submit to the camera tool after your translation is returned.</p>
      </Section>

      <Section title="Security">
        <p>We use reasonable safeguards, including encrypted (HTTPS) connections, to protect information. No method of transmission or storage is completely secure, so we can&rsquo;t guarantee absolute security.</p>
      </Section>

      <Section title="Your choices and rights">
        <p>You can ask us to access, correct or delete personal information we hold about you by emailing <a href={`mailto:${EMAIL}`}>{EMAIL}</a>. Depending on where you live (including Connecticut and other U.S. states with privacy laws), you may have additional rights, and we will honor them as the law requires. We won&rsquo;t discriminate against you for exercising them.</p>
      </Section>

      <Section title="Children">
        <p>The Service is not directed to children under 13, and we do not knowingly collect personal information from them. If you believe a child has sent us personal information, contact us and we will delete it.</p>
      </Section>

      <Section title="Changes to this policy">
        <p>We may update this policy from time to time. When we do, we&rsquo;ll change the &ldquo;Last updated&rdquo; date above, and significant changes will be noted on the site.</p>
      </Section>

      <Section title="Contact">
        <p>Questions or requests about privacy: <a href={`mailto:${EMAIL}`}>{EMAIL}</a>.</p>
      </Section>
    </LegalPage>
  );
}
